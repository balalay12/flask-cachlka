(function() {

	"use strict";

	angular
		.module("app")
		.factory("bodySizeFactory", function($resource) {

			function bodySize() {
				return $resource("/bodysize/:id", null, {
				    'update': {method: 'PATCH'}
				});
			}

			return {
				bodySize: bodySize
			}
		});
})();