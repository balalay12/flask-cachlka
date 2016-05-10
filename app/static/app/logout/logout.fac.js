(function() {

	"use strict";

	angular
		.module("app")
		.factory("logoutFactory", function($http) {

			function logout() {

				return $http.get("/account/logout/");
			}

			return {
				logout: logout
			}
		});
})();