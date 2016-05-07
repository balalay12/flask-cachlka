(function() {

	"use strict";

	angular
		.module("app")
		.directive("usernameUnique", function(registrationFactory) {

			return {
				restrict: "A",
				require: "ngModel",
				link: function(scope, element, attrs, ctrl) {
					scope.$watch(attrs.ngModel, function(value) {
						registrationFactory.check({"username": value})
							.success(function() {
								ctrl.$setValidity('unique-name', true);
							})
							.error(function() {
								ctrl.$setValidity('unique-name', false);
							});
					});
				}
			}
		})
		.directive("emailUnique", function(registrationFactory) {

			return {
				restrict: "A",
				require: "ngModel",
				link: function(scope, element, attrs, ctrl) {
					scope.$watch(attrs.ngModel, function(value) {
						registrationFactory.check({"email": value})
							.success(function() {
								ctrl.$setValidity('unique-email', true);
							})
							.error(function() {
								ctrl.$setValidity('unique-email', false);
							});
					});
				}
			}
		});
})();