(function() {
	
	"use strict";

	angular
		.module("app")
		.controller("registrationCtrl", function($state, registrationFactory) {

			var vm = this;

			vm.submit = submit;

			function submit() {

				var data = {reg: vm.new_user};

				registrationFactory.registration(data)
					.success(function() {
						$state.go("main.login");
					})
					.error(function() {
						if (status == '404') { $log.error(data); }
						if (status == '403') { vm.error = data['auth']; }
					});
			}
		});
})();