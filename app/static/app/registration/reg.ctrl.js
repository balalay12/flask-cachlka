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
					.error(function() {
						if (status == '404') { $log.error(data); }
						if (status == '403') { vm.error = data['auth']; }
					});
			}
		});
})();