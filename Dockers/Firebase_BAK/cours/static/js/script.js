let show_cards = () => {
	let cards = document.querySelectorAll(".course-card");
	cards.forEach((r, nb) => {
		if (nb > 5) r.classList.add("hidden");
	});
};

document.addEventListener("DOMContentLoaded", function () {
	const tabButtons = document.querySelectorAll(
		".bg-gray-100.rounded-full.p-1 button"
	);
	let nb;
	show_cards();
	tabButtons.forEach((button) => {
		button.addEventListener("click", function () {
			// Remove active class from all buttons
			tabButtons.forEach((btn) => {
				btn.classList.remove("bg-white", "text-gray-800", "shadow-sm");
				btn.classList.add("text-gray-600");
			});
			// Add active class to clicked button
			this.classList.add("bg-white", "text-gray-800", "shadow-sm");
			this.classList.remove("text-gray-600");
			document
				.querySelectorAll(".course-card")
				.forEach((r) => r.classList.add("hidden"));
			const fltId = this.getAttribute("data-filter");
			nb = 0;
			document.querySelectorAll(".course-card").forEach((r) => {
				if (r.getAttribute("genre").toLowerCase().includes(fltId) && nb < 6) {
					r.classList.remove("hidden");
					nb++;
				}
			});
			// show_cards();
		});
	});

	document.querySelectorAll('a.smooth-scroll[href^="#"]').forEach((link) => {
		link.addEventListener("click", function (e) {
			e.preventDefault();
			const targetId = this.getAttribute("href").substring(1); // remove the '#' symbol
			const targetElement = document.getElementById(targetId);
			if (targetElement) {
				targetElement.scrollIntoView({ behavior: "smooth" });
			}
		});
	});
});
