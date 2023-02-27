module.exports = {
    apps: [
      {
        name: "budget-diary",
        script:"run.sh",
        watch: 'budgetdiary/',
        ignore_watch: [
          "build",
          "dist",
          "*.pyc"
        ],
        env: {
          DB_USER : "root",
          DB_PASS : "",
          DB_HOST : "127.0.0.1:3306",
          DB_NAME : "budgetdiary"
        }
      }
    ],
  };
  