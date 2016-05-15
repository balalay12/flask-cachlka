(function() {

	'use strict';

	angular
		.module('app')
		.factory('addDayFactory', function($resource) {
			
			function addDay() {
				return $resource('/sets/');
			}

			return {
				addDay: addDay
			}
		})
})();