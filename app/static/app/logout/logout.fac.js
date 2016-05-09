(function() {

	"use strict";

	angular
		.module("app")
		.factory("logoutFactory", function($http) {

			function logout() {

				return $http.post("/api/logout");
			}

			return {
				logout: logout
			}
		});
})();