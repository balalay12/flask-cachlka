(function() {

	'use strict';

	angular
		.module('app')
		.controller('addExerciseCtrl', function($scope, $rootScope, $uibModalInstance, addDayFactory, categoryFactory, exerciseFactory) {

			$scope.day = $rootScope.addExercieDate;

			categoryFactory.categories()
				.get(function(data) {
					$scope.categories = data.categories;
				});

			$scope.$watch('cat', function(newVal, oldVal) {
				if(angular.isDefined(oldVal) | angular.isDefined(newVal)) {
					exerciseFactory.exercises_by_category()
						.get({id:newVal.category_id}, function(data) {
						$scope.exercises = data.exercises;
					});
				}
			});

			$scope.sets = [];
			$scope.addSet = function() {
				$scope.sets.push({weight: $scope.weight, repeats: $scope.repeats});
				$scope.weight = null;
				$scope.repeats = null;
				return $scope.sets
			};

			$scope.cancel = function() {
			    $uibModalInstance.close();
			};

			$scope.submit = function() {
				var set = [];
				set.push({'date':$scope.day, 'exercise':$scope.exercise.exercise_id, 'repeats': $scope.sets});
				addDayFactory.addDay()
					.save(set, function() {
						$rootScope.$broadcast('setsChanged');
						$scope.cancel();
					});
			};
		});
})();