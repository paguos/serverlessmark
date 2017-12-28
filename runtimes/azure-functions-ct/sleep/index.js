module.exports = function (context, req) {
  context.log('JavaScript HTTP trigger function processed a request.');
  if (req.query.seconds || (req.body && req.body.seconds)|| (req.body.seconds == 0)) {  
    context.res = {
          // status: 200, /* Defaults to 200 */
          body: ""
      };

  }
  else {
      context.res = {
          status: 400,
          body: "Please pass a message on the query string or in the request body"
      };
  }
  setTimeout(function(){context.done()}, req.body.seconds * 1000);
  
};