(function() {

	"use strict";

	angular
		.module("app")
		.factory("mainFactory", function($http) {

			function checkAuth() {

				return $http.post('api/check/auth/');
			}

			return {
				checkAuth: checkAuth
			}

		});
})();