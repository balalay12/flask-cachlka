(function() {

	"use strict";

	angular
		.module("app")
		.factory("registrationFactory", function($http) {

			function registration(data) {
				return $http.post("/reg/", angular.toJson(data))
			}

			function check(data) {
				return $http.post("/api/check/", angular.toJson(data));
			}

			return {
				registration: registration,
				check: check
			}
		});
})();