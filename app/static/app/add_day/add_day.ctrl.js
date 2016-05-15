(function() {

	'use strict';

	angular
		.module('app')
		.controller('addDayCtrl', function($scope, $rootScope, $filter, $uibModalInstance, categoryFactory, exerciseFactory, addDayFactory) {

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
				console.log('in function' + $scope.sets);
				$scope.weight = null;
				$scope.repeats = null;
				return $scope.sets
			};

			$scope.training = [];
			$scope.addExercise = function() {
				$scope.training.push({date:$filter('date')($scope.date, 'yyyy-MM-dd'), exercise: Number($scope.exercise.exercise_id), exercise_name: $scope.exercise.name, repeats: $scope.sets});
				$scope.exercise = null;
				$scope.sets = [];
			};

			$scope.submit = function() {
				addDayFactory.addDay()
					.save($scope.training, function() {
						$rootScope.$broadcast('dayAdded');
						$scope.cancel();
					});
			};

			$scope.cancel = function() {
				$uibModalInstance.dismiss('cancel');
			}


			// calendar
		      $scope.today = function() {
		        $scope.date = new Date();
		      };
		      $scope.today();

		      $scope.clear = function() {
		        $scope.date = null;
		      };

		      $scope.inlineOptions = {
		        customClass: getDayClass,
		        minDate: new Date(),
		        showWeeks: true
		      };

		      $scope.dateOptions = {
		        // dateDisabled: disabled,
		        formatYear: 'yy',
		        maxDate: new Date(2020, 5, 22),
		        minDate: new Date(),
		        startingDay: 1
		      };

		      // Disable weekend selection
		      function disabled(data) {
		        var date = data.date,
		        mode = data.mode;
		        return mode === 'day' && (date.getDay() === 0 || date.getDay() === 6);
		      }

		      $scope.toggleMin = function() {
		        $scope.inlineOptions.minDate = $scope.inlineOptions.minDate ? null : new Date();
		        $scope.dateOptions.minDate = $scope.inlineOptions.minDate;
		      };

		      $scope.toggleMin();

		      $scope.open = function() {
		        $scope.popup.opened = true;
		      };

		      $scope.setDate = function(year, month, day) {
		        $scope.date = new Date(year, month, day);
		      };

		      $scope.formats = ['dd-MMMM-yyyy', 'yyyy/MM/dd', 'dd.MM.yyyy', 'shortDate'];
		      $scope.format = 'dd.MM.yyyy';
		      $scope.altInputFormats = ['M!/d!/yyyy'];

		      $scope.popup = {
		        opened: false
		      };

		      var tomorrow = new Date();
		      tomorrow.setDate(tomorrow.getDate() + 1);
		      var afterTomorrow = new Date();
		      afterTomorrow.setDate(tomorrow.getDate() + 1);
		      $scope.events = [
		        {
		          date: tomorrow,
		          status: 'full'
		        },
		        {
		          date: afterTomorrow,
		          status: 'partially'
		        }
		      ];

		      function getDayClass(data) {
		        var date = data.date,
		        mode = data.mode;
		        if (mode === 'day') {
		          var dayToCheck = new Date(date).setHours(0,0,0,0);

		          for (var i = 0; i < $scope.events.length; i++) {
		              var currentDay = new Date($scope.events[i].date).setHours(0,0,0,0);

		            if (dayToCheck === currentDay) {
		              return $scope.events[i].status;
		            }
		          }
		        }

		        return '';
		      }
		});
})();