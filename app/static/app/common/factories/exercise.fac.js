(function() {

	'use strict';

	angular
		.module('app')
		.factory('exerciseFactory', function($resource) {

			function exercises() {
				return $resource('/api/exercises/');
			}

			return {
				exercises: exercises
			}
		});
})();