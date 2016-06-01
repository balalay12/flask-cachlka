(function() {

    'use strict';

    angular
        .module('app')
        .controller('changePasswordCtrl', function($scope, $http) {

            $scope.submit = function() {
                var data = {'old': $scope.old_password, 'new': $scope.new_password, 'confirm': $scope.confirm_password}
                $http.post('/account/change_password/', angular.toJson(data))
                .success(function() {

                })
                .error(function(data) {
                    $scope.error = data.error;
                })
            }
        })
})();