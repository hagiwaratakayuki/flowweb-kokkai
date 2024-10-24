const fs = require('fs');
const env = fs.readFileSync('./env.sh', {endcoding:'utf8'});
const template = fs.readFileSync('./gceenv_template.txt');
const gceenv = template.replace('#env#', env);
fs.writeFileSync('./gceenv.sh', gceenv)
