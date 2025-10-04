import { Volume2 } from 'lucide-react';

interface AudioPlayerProps {
  audioUrl: string;
  label: string;
}

export function AudioPlayer({ audioUrl, label }: AudioPlayerProps) {
  return (
    <div className="flex items-center gap-3 p-3 rounded-lg bg-gray-50 dark:bg-darkGray border border-gray-200 dark:border-teal/30">
      <Volume2 className="w-5 h-5 text-teal dark:text-gold flex-shrink-0" />
      <div className="flex-1 min-w-0">
        <p className="text-sm font-medium text-gray-700 dark:text-offWhite mb-1">
          {label}
        </p>
        <audio
          controls
          className="w-full h-8"
          style={{
            filter: 'hue-rotate(180deg) saturate(0.8)',
          }}
        >
          <source src={audioUrl} type="audio/mpeg" />
          Your browser does not support the audio element.
        </audio>
      </div>
    </div>
  );
}
