(function() {

	"use strict";

	angular
		.module("app")
		.factory("mainFactory", function($http) {

			function checkAuth() {

				return $http.get('/account/check_auth/');
			}

			return {
				checkAuth: checkAuth
			}

		});
})();