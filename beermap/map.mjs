const iframe = document.querySelector('iframe[title="Beer Map"]');
const source = new URL(iframe.dataset.src, document.baseURI);
let attachedDocument = null;

function restoreMapLocation() {
	const destination = new URL(source);
	destination.search = location.search;
	destination.searchParams.set("data", source.searchParams.get("data"));
	destination.hash = location.hash;
	if (iframe.contentWindow.location.href === "about:blank") {
		iframe.src = destination.href;
	} else if (iframe.contentWindow.location.href !== destination.href) {
		iframe.contentWindow.location.replace(destination.href);
	}
}

function synchronizeMapLocation() {
	const destination = new URL(location.href);
	destination.search = iframe.contentWindow.location.search;
	destination.searchParams.delete("data");
	destination.hash = iframe.contentWindow.location.hash;
	if (destination.href !== location.href) {
		history.replaceState(history.state, "", destination.href);
	}
}

const attachMapLocation = () => {
	if (iframe.contentWindow.location.pathname !== source.pathname) return;
	if (attachedDocument === iframe.contentDocument) return;
	attachedDocument = iframe.contentDocument;
	const embeddedHistory = iframe.contentWindow.history;
	const replaceState = embeddedHistory.replaceState.bind(embeddedHistory);
	embeddedHistory.replaceState = (state, title, address) => {
		replaceState(state, title, address);
		synchronizeMapLocation();
	};
	iframe.contentWindow.addEventListener("hashchange", synchronizeMapLocation);
	synchronizeMapLocation();
};

iframe.addEventListener("load", attachMapLocation);
window.addEventListener("popstate", restoreMapLocation);
window.addEventListener("hashchange", restoreMapLocation);
restoreMapLocation();
if (iframe.contentDocument.readyState === "complete") attachMapLocation();
