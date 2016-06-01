(function() {

	"use strict";

	angular
		.module("app")
		.controller("profileCtrl", function($scope, $uibModal, $rootScope, profileFactory, bodySizeFactory) {

			var vm = this;

			vm.addBodySize = addBodySize;
			vm.editBodySize = editBodySize;
			vm.changePassword = changePassword;

			profileFactory.userProfile()
				.get(function(data) {
					vm.user = data;
				});

			var bodySizeQuery = function() {
				bodySizeFactory.bodySize()
					.get(function(data) {
						vm.bodySize = data.body_size;
					});
			}
			bodySizeQuery();

			$scope.$on("bodySizeEdited", function() {
				bodySizeQuery();
			});

			function addBodySize() {
				$rootScope.bodySizeId = null;
				var addBodySizeModal = $uibModal.open({
					templateUrl: template_dirs + "/bodysize/body_size.html",
					controller: "bodySizeCtrl"
				});
			}

			function editBodySize(id) {
				$rootScope.bodySizeId = id;
				var editBodySizeModal = $uibModal.open({
					templateUrl: template_dirs + "/bodysize/body_size.html",
					controller: "bodySizeCtrl"
				})
			}

			function changePassword() {
			    var changePasswordModel = $uibModal.open({
			        templateUrl: template_dirs + "/profile/change_password/change_password.html",
			        controller: "changePasswordCtrl"
			    })
			}

		});
})();
