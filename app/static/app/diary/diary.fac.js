(function() {

	'use strict';

	angular
		.module('app')
		.factory('setsFactory', function($resource) {

			return $resource('/sets/:month/:year', null, {
				'getAllSets': {
					method: 'GET',
					isArray: false
				}
			})
		});
})();