# Importing JS modules without specifying export

https://stackoverflow.com/questions/38172337/using-require-without-export

In `dpe-api/src/server.js`, we directly require the `index.js` file of `@bbc/digital-paper-edit-api`.
The `index.js` does not specify any exports, so how does it work?

In JS, when one imports a module without an export, the module is still run. This is how `@bbc/digital-paper-edit-api` can simply run without explicitly being assigned and executed. Since the aforementioned dependency also relies on variables such as `process.env.PORT` to specify the behaviour of the Express server, we can pass the variables in, like `PORT=4000 npm start` to start the server at the specified port.

The caveat with this way of importing / exporting is that it is not possible to access the variables inside the imported dependencies. If you want to actually interact with the variables inside the module, export them. Another more dangerous aspect of this is that when a variable is not assigned with `var` in the imported dependency, it is treated as a global variable. So there are dangers of hidden overwriting of variables. It's not recommended.
