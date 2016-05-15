(function() {

	'use strict';

	angular
		.module('app')
		.factory('exerciseFactory', function($resource) {

			function exercises() {
				return $resource('/exercises/:id', null);
			}

			function exercises_by_category() {
				return $resource('/exercises/exercises_by_category/:id', null);
			}

			return {
				exercises: exercises,
				exercises_by_category: exercises_by_category
			}
		});
})();