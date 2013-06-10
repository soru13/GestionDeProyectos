/*function route(handle, pathname, response, postData) {
  console.log("A punto de rutear una peticion para " + pathname);
  if (typeof handle[pathname] === 'function') {
    handle[pathname](response, postData);
  } else {
    console.log("No se ha encontrado manipulador para " + pathname);
    response.writeHead(404, {"Content-Type": "text/html"});
    response.write("404 No encontrado");
    response.end();
  }
}

exports.route = route;*/
var website = require('./controllers/website'),
    admin = require('./controllers/admin');

function is_admin(req, res, next) {
  if(req.user && req.user.admin) {
    next();
  } else {
    res.redirect('/');
  }
}

module.exports = function (app, passport) {

  /*
   * Website urls
   */
  app.get('/', website.index);
  app.post('/feedback', website.feedback);
  app.get('/salir', website.salir);

  /*
   * Admin urls
   */
  app.get('/admin',          is_admin, admin.index);
  app.get('/admin/feedback', is_admin, admin.feedback);
  app.get('/admin/feedback/:date', is_admin, admin.feedback_single);
  app.get('/admin/users',    is_admin, admin.users);

  app.post('/admin/update',  is_admin, admin.update);
  /*
   * Passport urls
   */
  // Twitter
  app.get('/auth/twitter', passport.authenticate('twitter'));
  app.get('/auth/twitter/callback',
    passport.authenticate('twitter', { successRedirect: '/',
                                       failureRedirect: '/' }));
  // Facebook
  app.get('/auth/facebook', passport.authenticate('facebook'));
  app.get('/auth/facebook/callback',
    passport.authenticate('facebook', { successRedirect: '/',
                                       failureRedirect: '/' }));


  app.all('*', website.notFound);
};