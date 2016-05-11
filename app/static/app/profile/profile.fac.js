(function() {

	"use strict";

	angular
		.module("app")
		.factory("profileFactory", function($resource) {
			
			function userProfile() {
				return $resource("/profile/");
			}

			return {
				userProfile: userProfile
			}
		});
})();