(function() {

	"use strict";

	angular
		.module("app")
		.factory("registrationFactory", function($http) {

			function registration(data) {
				return $http.post("/account/registration/", angular.toJson(data))
			}

			function check(data) {
				return $http.post("/account/check_unique/", angular.toJson(data));
			}

			return {
				registration: registration,
				check: check
			}
		});
})();