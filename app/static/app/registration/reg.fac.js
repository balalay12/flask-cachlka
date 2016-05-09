(function() {

	"use strict";

	angular
		.module("app")
		.factory("registrationFactory", function($http) {

			function registration(data) {
				return $http.post("/api/reg", angular.toJson(data))
			}

			function check(data) {
				return $http.post("/api/check_unique", angular.toJson(data));
			}

			return {
				registration: registration,
				check: check
			}
		});
})();