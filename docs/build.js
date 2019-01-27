const fs = require('fs');
const showdown = require('showdown');
const mustache = require('mustache');

const converter = new showdown.Converter({ tables: true });

const ctx = {
    version: 'v0.1.1'
};

fs.readdirSync('./content').forEach(file => {
    ctx[file.replace('.md', '')] = converter.makeHtml(fs.readFileSync('./content/' + file, 'utf8'));
});

const index = fs.readFileSync('./templates/index.mustache', 'utf8');
fs.writeFileSync('./index.html', mustache.render(index, ctx));