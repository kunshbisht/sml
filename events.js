[...document.getElementsByTagName('*')]
	.filter(el => /^on/i.test(el.tagName))
	.forEach(el => {
		const fn = new Function(el.textContent);
		const eventName = el.tagName.slice(2).toLowerCase();
		el.parentElement.addEventListener(eventName, fn);
		el.remove();
	});
