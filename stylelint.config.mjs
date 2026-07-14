/** @type {import("stylelint").Config} */
export default {
	extends: ["stylelint-config-standard"],
	// The submodule's CSS is owned (and linted) by its own repo; enforcing this
	// repo's rules on it lets an upstream bump break CI here.
	ignoreFiles: ["untappd-data-parser/**", "node_modules/**"],
	rules: {
		"no-descending-specificity": null,
		// Range notation (width <= 600px) is dropped wholesale by Safari <= 16.3 and
		// Chrome <= 103, silently disabling mobile styles; require the classic prefix form.
		"media-feature-range-notation": "prefix",
	},
};
