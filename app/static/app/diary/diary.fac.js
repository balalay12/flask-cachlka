(function() {

	'use strict';

	angular
		.module('app')
		.factory('setsFactory', function($resource) {

			return $resource('/sets/:id', null, {
				'getAllSets': {
					url: '/sets/by_date/:date',
					method: 'GET',
					isArray: false
				},
				'updateSet': {
				    url: '/sets/:id',
				    method: 'PATCH'
				}
			})
		});
})();