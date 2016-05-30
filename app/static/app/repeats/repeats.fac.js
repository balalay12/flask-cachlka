(function() {

    'use strict';

    angular
        .module('app')
        .factory('repeatsFactory', function($resource) {

            function repeats() {
                return $resource('/repeats/:id', null, {
                    'update': {method: 'PATCH'}
                });
            }

            return {
                repeats: repeats
            }
        });
})();