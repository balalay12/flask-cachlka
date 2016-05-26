(function() {

	'use strict';

	angular
		.module('app')
		.controller('editExerciseCtrl', function($scope, $rootScope, $filter, $uibModalInstance, categoryFactory, exerciseFactory, setsFactory) {

			categoryFactory.categories()
				.get(function(data) {
					$scope.categories = data.categories;
				});

			setsFactory.getSet({id: $rootScope.editSetId}, function(data) {
			    $scope.cat = {category_id:data.set.items.category_id, name:data.set.items.category_name};
				$scope.exercise = {exercise_id: data.set.items.exercise_id, name:data.set.items.exercise_name};
				$scope.date = new Date(data.set.date);
			});

			$scope.$watch('cat', function(newVal, oldVal) {
				if(angular.isDefined(oldVal) | angular.isDefined(newVal)) {
					exerciseFactory.exercises_by_category()
						.get({id:newVal.category_id}, function(data) {
						$scope.exercises = data.exercises;
					});
				}
			});

			$scope.cancel = function() {
			    $uibModalInstance.close();
			};

			$scope.delete = function() {
			    setsFactory.delete({id: $rootScope.editSetId}, function() {
					$rootScope.$broadcast('setsChanged');
					$scope.cancel();
			    });
			};

			$scope.submit = function() {
				var upd_exercise = {'exercise': $scope.exercise.exercise_id};
				setsFactory.updateSet({id: $rootScope.editSetId}, upd_exercise, function() {
					$rootScope.$broadcast('setsChanged');
					$scope.cancel();;
				});
			}

		});
})();