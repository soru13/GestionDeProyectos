/*// Cargamos módulos Node

var cluster = require('cluster');
var url = require("url");
var numCPUs = require('os').cpus().length;
// Creamos aplicación

var http = require('http');

if (cluster.isMaster) { 
// Fork workers.
require('os').cpus().forEach(function(){
cluster.fork();
});
// In case the worker dies!
cluster.on('exit', function(worker, code, signal) {
console.log('worker ' + worker.process.pid + ' died');
});
// As workers come up.
cluster.on('listening', function(worker, address) {
console.log("A worker with #"+worker.id+" is now connected to " +address.address +":" + address.port);
});
// When the master gets a msg from the worker increment the request count.
var reqCount = 0;
Object.keys(cluster.workers).forEach(function(id) {
cluster.workers[id].on('message',function(msg){
if(msg.info && msg.info == 'ReqServMaster'){
reqCount += 1;
}
});
});
// Track the number of request served.
setInterval(function() {
console.log("Number of request served = ",reqCount);
}, 1000);
function iniciar(route, handle) {
  function onRequest(request, response) {
        var dataPosteada = "";
        var pathname = url.parse(request.url).pathname;
        console.log("Peticion para " + pathname + " recibida.");

        request.setEncoding("utf8");
          request.addListener("data", function(trozoPosteado) {
          dataPosteada += trozoPosteado;
          console.log("Recibido trozo POST '" + trozoPosteado + "'.");
          
    });

    request.addListener("end", function() {
      route(handle, pathname, response, dataPosteada);
    });

  }
  console.log("Servidor Iniciado");
}
exports.iniciar = iniciar;
} else {
function iniciar(route, handle) {
  function onRequest(request, response) {
        var dataPosteada = "";
        var pathname = url.parse(request.url).pathname;
        console.log("Peticion para " + pathname + " recibida.");

        request.setEncoding("utf8");

        request.addListener("data", function(trozoPosteado) {
          dataPosteada += trozoPosteado;
          console.log("Recibido trozo POST '" + trozoPosteado + "'.");
    });

    request.addListener("end", function() {
      route(handle, pathname, response, dataPosteada);
    });

  }

  http.createServer(onRequest).listen(8888);
  console.log("Servidor Iniciado");
}
exports.iniciar = iniciar;
}
*/

/*
var fs = require('fs'),
  cluster = require('cluster'),
  config = require('./config');


if(cluster.isMaster) {
  for(var i = 0; i < require('os').cpus().length; i++) {
    cluster.fork();
  }

  cluster.on('exit', function (worker, code, signal) {
    console.log('worker ' + worker.process.pid + ' died');
    cluster.fork();
    console.log('worker restarted');
  });
} else {
  // aplication
  var app = require('./app')(config),
    sessionStore = app.sessionStore;
  app = app.app;
  /*
  * Server configuration
  *//*
  var server = config.secure ? require('https').createServer({key: fs.readFileSync(config.key).toString(),
      cert: fs.readFileSync(config.cert).toString()}, app) : require('http').createServer(app);

  // io
  require('./io')(config, server, sessionStore);

  /*
  * Bootstrap
  *//*
  server.listen(config.port, function(){
    console.log("Mejorando.la Chat server listening on port ");
  });
}*/
var express = require('express'),
  app     = express(),
  server  = require('http').createServer(app),
  io      = require('socket.io').listen(server),
  cons    = require('consolidate');

server.listen(8888);

app.engine('.html', cons.jade);
app.set('view engine', 'html');

app.use(express.static('./public'));

app.get('/', function(req, res){
    res.render('index',{
      titulo : "Hola"
    });
});
//JSON para controlar que no se repitan nombres
var usuariosConectados = {};
var usuariosConectadosID = {};
var sockets =  {};
io.sockets.on('connection', function (socket) {
      //Recibimos el nombre
      socket.on("enviarNombre",function(dato,userID)
      {
        //Verificamos que ese nombre no existe
        if(usuariosConectados[dato])
        {
          socket.emit("errorName");
        }
        else
        {
          //Lo asignamos a la socket y lo agregamos
          socket.nickname = dato;
          usuariosConectados[dato] = socket.nickname;
          usuariosConectadosID[dato] = userID;
          sockets[userID] = socket.id;
        }
        data = [dato,usuariosConectados,usuariosConectadosID,sockets];
        //Enviamos los datos de regreso a las sockets
        io.sockets.emit("mensaje",data);
      }); 
      //Recibimos un nuevo msj y lo mandamos a todas las sockets
      socket.on("enviarMensaje",function(mensaje,tokenSocked,tokenSockedlocal,img)
      {
        console.log("mensaje "+mensaje);
        var data = [img,' '+socket.nickname+' : </span>',mensaje];
        //socket.broadcast.emit('newMessage', data);//a todos menos al que envio
        io.sockets.socket(tokenSocked).emit('newMessage', data,tokenSockedlocal,socket.nickname);
        //io.sockets.emit("newMessage",data);//atodos incluyendo al que envio
      });
      //Se dispara cuando una socket se desconecta
      socket.on('disconnect', function () 
      {
        //Eliminamos al usuario de los conectados
        delete usuariosConectados[socket.nickname];
        //Creamos un arreglo con los usuarios y el que se eliminó
        data = [usuariosConectados,socket.nickname];
        console.log(data);
        //Mandamos la información a las Sockets
        io.sockets.emit("usuarioDesconectado",data);
      });
});




