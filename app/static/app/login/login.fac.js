(function() {

	"use strict";

	angular
		.module("app")
		.factory("loginFactory", function($http) {

			function login(data) {

				return $http.post("/account/login/", angular.toJson(data));
			}

			return {
				login: login
			}
		});
})();