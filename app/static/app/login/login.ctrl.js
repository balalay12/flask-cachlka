(function() {

	"use strict";

	angular
		.module("app")
		.controller("loginCtrl", function($scope, $state, loginFactory) {

			var vm = this;

			vm.submit = submit;

			function submit() {
				
				loginFactory.login(vm.user)
					.success(function() {
						$scope.$emit("userIn");
						$state.go("home.news");
					})
					.error(function(data, status) {
						if (status == '404') { $scope.error = data['error']; }
						if (status == '403') { $scope.error = data['auth']; }
					});
			}
		});
})();