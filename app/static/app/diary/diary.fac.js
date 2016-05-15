(function() {

	'use strict';

	angular
		.module('app')
		.factory('setsFactory', function($resource) {

			return $resource('/sets/', {}, {
				'getAllSets': {
					method: 'GET',
					isArray: false
				}
			})
		});
})();