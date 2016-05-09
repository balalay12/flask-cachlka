(function() {

	"use strict";

	angular
		.module("app")
		.controller("logoutCtrl", function($scope, $state, logoutFactory) {

			logoutFactory.logout()
				.success(function() {
					$scope.$emit("userOut");
					$state.go("home.news");
				})
				.error(function() {
					console.log("что-то пошло не так")
				});
		});
})();