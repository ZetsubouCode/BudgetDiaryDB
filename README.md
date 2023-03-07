# BudgetDiaryDB
I separating db functionality from the base code, for code clarity purposes

# Deploy on Niagahoster tutorial
1. Set up database
- Create database
- Create user
- import your sql

2. Clone repo
- Create .cpanel

3. Set up pm2
- Create new node.js web app, put it outside public_html
- Create new package.json file inside your working directory
- View your node.js web app, it should displaying "run NPM install". Press that to install NPM
- Go to terminal and enter your node.js virtual env
- Install npm like usual using "npm install pm2"
- Your pm2 are ready to use. Note that you should use npx instead of npm when accessing pm2

4. Adjust config file
- Edit your run.sh file to 
```
cd /home/[niagahoster username]/[path to cloned repo] 
### Example -> cd /home/u6969690/public_html/budget-diary
~/virtualenv/[path to cloned repo]/[your python version]/bin/python3 -m uvicorn [file/folder that included FastAPI obj]:[FastAPI obj] --port [desired port]
### Example -> ~/virtualenv/public_html/budget-diary/3.10/bin/python3 -m uvicorn pjtki:app --port 55002
```
- Edit your ecosystem.config.js, just the script part
```
script:"../[path to cloned repo]/[your script name]"
### Example -> script:"../public_html/backend-pjtki/run.sh"
```

6. Run project
