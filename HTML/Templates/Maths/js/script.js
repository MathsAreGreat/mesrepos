document.addEventListener("DOMContentLoaded", function () {
	const tabButtons = document.querySelectorAll(
		".bg-gray-100.rounded-full.p-1 button"
	);
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
		});
	});
});
