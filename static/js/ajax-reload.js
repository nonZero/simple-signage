'use strict';
const URL = "/api/content/";

$(function () {
	const loadInfo = function (url, el, timeout) {
		el.removeClass(['flash', 'error']);
		$.get(url).done(function (resp) {
			el.html(resp.trim()).addClass('flash');
		}).fail(function (resp) {
			el.html("ERROR!").addClass('error');
		}).always(function () {
			setTimeout(function () {
				loadInfo(url, el, timeout);
			}, timeout);
		})
	};

	loadInfo(URL, $("#info1"), 2000);
	loadInfo(URL, $("#info2"), 3100);
	loadInfo(URL, $("#info3"), 4200);
});
