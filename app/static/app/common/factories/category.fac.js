(function() {

	'use strict';

	angular
		.module('app')
		.factory('categoryFactory', function($resource) {

			function categories() {
				return $resource('/api/categories/');
			}

			return {
				categories: categories
			}
		})
})();