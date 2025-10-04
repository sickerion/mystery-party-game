import type { GenerationStep } from '@/types';

interface StepIndicatorProps {
  currentStep: GenerationStep;
}

const steps: { id: GenerationStep; label: string }[] = [
  { id: 'initial', label: 'Game Details' },
  { id: 'characters', label: 'Characters' },
  { id: 'plot', label: 'Plot' },
  { id: 'clues', label: 'Clues' },
  { id: 'metadata', label: 'Metadata' },
  { id: 'validation', label: 'Validation' },
];

export function StepIndicator({ currentStep }: StepIndicatorProps) {
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
                    ? 'bg-teal text-offWhite'
                    : 'bg-darkGray text-lightGray'
                }`}
              >
                {index + 1}
              </div>
              <p className={`text-xs mt-2 ${index <= currentStepIndex ? 'text-offWhite' : 'text-lightGray'}`}>
                {step.label}
              </p>
            </div>
            {index < steps.length - 1 && (
              <div
                className={`absolute top-5 left-1/2 w-full h-0.5 ${
                  index < currentStepIndex ? 'bg-gold' : 'bg-darkGray'
                }`}
              />
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
