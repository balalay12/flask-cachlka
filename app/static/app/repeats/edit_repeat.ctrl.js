(function() {

    'use strict';

    angular
        .module('app')
        .controller('editRepeatCtrl', function($scope, $rootScope, $uibModalInstance, repeatsFactory) {

            $scope.adding = false;
            $scope.title = 'Изменить подход';
            console.log($rootScope.editRepeatId);

            repeatsFactory.repeats()
                .get({id: $rootScope.editRepeatId}, function(data) {
                    $scope.set = data.repeat;
                });

            $scope.cancel = function() {
                $uibModalInstance.close();
            };

            $scope.submit = function() {
                repeatsFactory.repeats()
                    .update({id: $rootScope.editRepeatId}, $scope.set, function() {
                        $rootScope.$broadcast('setsChanged');
                        $scope.cancel();
                    })
            };

            $scope.delete = function() {
                repeatsFactory.repeats()
                    .delete({id: $rootScope.editRepeatId}, function() {
                        $rootScope.$broadcast('setsChanged');
                        $scope.cancel();
                    });
            }
        });
})();