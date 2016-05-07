(function() {

	"use strict";

	angular
		.module("app")
		.controller("mainCtrl", function($scope, $http, mainFactory) {

			var nav = this;
			
			var viewItems = function(bool) {
				nav.auth = bool;
			}

			mainFactory.checkAuth()
				.success(function() {
					viewItems(true);
				})
				.error(function() {
					viewItems(false);
				});

			$scope.$on('userIn', function() {
				viewItems(true);
			});

			$scope.$on('userOut', function() {
				viewItems(false);
			});
		});
})();