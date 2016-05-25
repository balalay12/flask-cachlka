(function() {

	'use strict';

	angular
		.module('app')
		.controller('viewDayCtrl', function($scope, $rootScope,$stateParams, $uibModal, setsFactory) {

			var vm = this;
			vm.addExercise = addExercise;
			vm.editExercise = editExercise;
			vm.addRepeat = addRepeat;
			vm.editRepeat = editRepeat;

			console.log($stateParams.date);

			function allSets() {
				setsFactory.getAllSets({date: $stateParams.date}, function(data) {
					vm.sets = data.day;
				});
			}
			allSets();

			$scope.$on('setsChanged', function() {
				allSets();
			});

			function addExercise(_date) {
				$rootScope.addExercieDate = _date;
				var addExercieModal = $uibModal.open({
					templateUrl: template_dirs + '/exercises/add_exercise.html',
					controller: 'addExerciseCtrl'
				});
			}

			function editExercise(set_id) {
				$rootScope.editSetId = set_id;
				var editExercieModal = $uibModal.open({
					templateUrl: template_dirs + '/exercises/edit_exercise.html',
					controller: 'editExerciseCtrl'
				});
			}

			function addRepeat(set_id) {
				$rootScope.addRepeatToSetId = set_id;
				var addRepeatModal = $uibModal.open({
					templateUrl: template_dirs + '/repeats/repeat.html',
					controller: 'addRepeatCtrl'
				})
			}

			function editRepeat(repeat_id) {
				$rootScope.editRepeatId = repeat_id;
				var editRepeatModal = $uibModal.open({
					templateUrl: template_dirs + '/repeats/repeat.html',
					controller: 'editRepeatCtrl'
				})
			}
		})
})();