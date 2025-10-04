import { useTranslation } from 'react-i18next';
import type { GenerationStep } from '@/types';

interface StepIndicatorProps {
  currentStep: GenerationStep;
}

export function StepIndicator({ currentStep }: StepIndicatorProps) {
  const { t } = useTranslation();

  const steps: { id: GenerationStep; label: string }[] = [
    { id: 'initial', label: t('wizard.steps.details') },
    { id: 'characters', label: t('wizard.steps.characters') },
    { id: 'plot', label: t('wizard.steps.plot') },
    { id: 'clues', label: t('wizard.steps.clues') },
    { id: 'metadata', label: t('wizard.steps.metadata') },
    { id: 'validation', label: t('wizard.steps.validation') },
  ];

  const currentStepIndex = steps.findIndex(s => s.id === currentStep);

  return (
    <div className="mb-8">
      <div className="flex items-center justify-between">
        {steps.map((step, index) => (
          <div key={step.id} className="flex-1 relative">
            <div className="flex flex-col items-center">
              <div
                className={`w-10 h-10 rounded-full flex items-center justify-center font-semibold ${
                  index < currentStepIndex
                    ? 'bg-gold text-navy'
                    : index === currentStepIndex
                    ? 'bg-teal text-white'
                    : 'bg-gray-300 text-gray-600 dark:bg-darkGray dark:text-lightGray'
                }`}
              >
                {index + 1}
              </div>
              <p className={`text-xs mt-2 ${index <= currentStepIndex ? 'text-darkText dark:text-offWhite' : 'text-gray-500 dark:text-lightGray'}`}>
                {step.label}
              </p>
            </div>
            {index < steps.length - 1 && (
              <div
                className={`absolute top-5 left-1/2 w-full h-0.5 ${
                  index < currentStepIndex ? 'bg-gold' : 'bg-gray-300 dark:bg-darkGray'
                }`}
              />
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
