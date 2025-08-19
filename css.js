[...document.getElementsByTagName('css')].forEach(el => {
    let style = el.textContent
        .replace(/\s+/g, ' ')
        .trim();

    // simple regex for { prop: value; ... }
    if (!/^\{\s*([-a-zA-Z_]+:[^;]+;\s*)*\}$/.test(style)) {
        throw new SyntaxError("Invalid CSS block");
    }

    // remove braces
    style = style.replace(/^\{|\}$/g, '').trim();

    // split key/value
    style.split(';').forEach(line => {
        if (!line.trim()) return;
        const colonIndex = line.indexOf(':');
        if (colonIndex === -1) return;
        const key = line.slice(0, colonIndex).trim();
        const value = line.slice(colonIndex + 1).trim();
		el.parentElement.style[key] = value;
    });
	
	el.remove()
});
