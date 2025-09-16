window.MathJax = {
	tex: {
		inlineMath: [
			["$", "$"],
			["\\(", "\\)"],
		],
	},
	svg: { fontCache: "global" },
};

(function () {
	var script = document.createElement("script");
	script.src = "http://localhost/mathjax/es5/tex-chtml-full.js";
	script.async = true;
	document.head.appendChild(script);
})();
