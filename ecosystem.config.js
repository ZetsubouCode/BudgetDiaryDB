module.exports = {
    apps: [
      {
        name: "budget-diary",
        script:"../public_html/BudgetDiaryDB/run.sh",
        watch: 'budgetdiary/',
        ignore_watch: [
          "build",
          "dist",
          "*.pyc"
        ],
        env: {
          DB_USER : "u1572803_kevin",
          DB_PASS : "kevinkevinkevin",
          DB_HOST : "127.0.0.1:3306",
          DB_NAME : "budgetdiary",
          SALT : "kotajenaka"
        }
      }
    ],
  };
  
