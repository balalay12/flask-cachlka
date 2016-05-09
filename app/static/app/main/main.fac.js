(function() {

	"use strict";

	angular
		.module("app")
		.factory("mainFactory", function($http) {

			function checkAuth() {

				return $http.post('api/check_auth');
			}

			return {
				checkAuth: checkAuth
			}

		});
})();