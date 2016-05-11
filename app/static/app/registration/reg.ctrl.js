(function() {
	
	"use strict";

	angular
		.module("app")
		.controller("registrationCtrl", function($state, registrationFactory) {

			var vm = this;

			vm.submit = submit;

			function submit() {

				registrationFactory.registration(vm.new_user)
					.success(function() {
						$state.go("login");
					})
					.error(function(data, status) {
						if (status == '404') { vm.error = data['error']; }
						if (status == '409') { vm.error = data['auth']; }
					});
			}
		});
})();