[...document.getElementsByTagName('xcs')].forEach(el => {
	el.textContent.trim().split(/\s+/).forEach(tok => {
		if (/^[a-z]+[-\d].*$/i.test(tok)) shorthand(tok)
		else property(tok)
	});

	function shorthand(tok) {
		const shorthands = {
			m: 'margin',
			mt: 'margin-top',
			mr: 'margin-right',
			mb: 'margin-bottom',
			ml: 'margin-left',
			p: 'padding',
			pt: 'padding-top',
			pr: 'padding-right',
			pb: 'padding-bottom',
			pl: 'padding-left',
			w: 'width',
			h: 'height',
			bg: 'background',
			c: 'color',
			fs: 'font-size',
			fw: 'font-weight',
			lh: 'line-height',
			bs: 'box-shadow',
			br: 'border-radius',
			bc: 'border-color',
			bw: 'border-width',
			bt: 'border-top',
			brd: 'border',
			d: 'display',
			zi: 'z-index',
			ta: 'text-align',
			td: 'text-decoration',
			ts: 'text-shadow',
			o: 'opacity'
		};

		let [key, ...parts] = tok.split("-");
		let cssProp = shorthands[key] || key;

		// normalize values: numbers → add px
		const values = parts.map(v => /^\d+$/.test(v) ? v + "px" : v);

		el.parentElement.style[toCamel(cssProp)] = values.join(" ");
	}

	function property(tok) {
		const attrs = {
			flex: ['display', 'flex'],
			grid: ['display', 'grid'],
			block: ['display', 'block'],
			inline: ['display', 'inline'],
			inlineblock: ['display', 'inline-block']
		};
		if (!Object.hasOwn(attrs, tok)) throw SyntaxError(`${tok} is not a key`);
		el.parentElement.style[attrs[tok][0]] = attrs[tok][1];
	}

	function toCamel(str) {
		return str.replace(/-([a-z])/g, (_, c) => c.toUpperCase());
	}

	el.remove()
});
