(function() {

    'use strict';

    angular
        .module('app')
        .controller('addRepeatCtrl', function($scope, $rootScope, $uibModalInstance, repeatsFactory) {

            $scope.adding = true;
            $scope.title = 'Добавить подход';

            $scope.cancel = function() {
                $uibModalInstance.close();
            }

            $scope.submit = function() {
                $scope.set['set'] = $rootScope.addRepeatToSetId;
                console.log($scope.set);
                repeatsFactory.repeats()
                    .save($scope.set, function() {
                        $rootScope.$broadcast('setsChanged');
                        $scope.cancel();
                    });
            };
        });
})();