/**
 * Solutions — CDK TypeScript Exercises
 * Try solving the exercises first! Only look here when stuck.
 *
 * RUN: cd typescript/cdk && npx tsx solutions/all_solutions.ts
 *
 * Each section is wrapped in `{ ... }` so identically-named classes/consts
 * (StorageStack, app, template, ...) don't collide across sections.
 */

import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as glue from 'aws-cdk-lib/aws-glue';
import * as sfn from 'aws-cdk-lib/aws-stepfunctions';
import * as tasks from 'aws-cdk-lib/aws-stepfunctions-tasks';
import { Template } from 'aws-cdk-lib/assertions';

// =====================================================================
// 01 — StorageStack
// =====================================================================
{
  interface StorageStackProps extends cdk.StackProps {}

  class StorageStack extends cdk.Stack {
    readonly rawBucket: s3.Bucket;
    readonly processedBucket: s3.Bucket;
    readonly scriptsBucket: s3.Bucket;

    constructor(scope: Construct, id: string, props?: StorageStackProps) {
      super(scope, id, props);

      this.rawBucket = new s3.Bucket(this, 'RawBucket', {
        versioned:         true,
        removalPolicy:     cdk.RemovalPolicy.DESTROY,
        autoDeleteObjects: true,
      });

      this.processedBucket = new s3.Bucket(this, 'ProcessedBucket', {
        versioned:         true,
        removalPolicy:     cdk.RemovalPolicy.DESTROY,
        autoDeleteObjects: true,
        lifecycleRules: [
          {
            transitions: [
              { storageClass: s3.StorageClass.INFREQUENT_ACCESS, transitionAfter: cdk.Duration.days(30) },
            ],
          },
        ],
      });

      this.scriptsBucket = new s3.Bucket(this, 'ScriptsBucket', {
        versioned:         false,
        removalPolicy:     cdk.RemovalPolicy.DESTROY,
        autoDeleteObjects: true,
      });

      new cdk.CfnOutput(this, 'RawBucketName',       { value: this.rawBucket.bucketName });
      new cdk.CfnOutput(this, 'ProcessedBucketName', { value: this.processedBucket.bucketName });
      new cdk.CfnOutput(this, 'ScriptsBucketName',   { value: this.scriptsBucket.bucketName });
    }
  }

  const app = new cdk.App();
  const storage = new StorageStack(app, 'TestStorage');
  const template = Template.fromStack(storage);

  template.resourceCountIs('AWS::S3::Bucket', 3);

  template.hasResourceProperties('AWS::S3::Bucket', {
    VersioningConfiguration: { Status: 'Enabled' },
  });

  template.hasResourceProperties('AWS::S3::Bucket', {
    LifecycleConfiguration: {
      Rules: [
        {
          Transitions: [
            { StorageClass: 'STANDARD_IA', TransitionInDays: 30 },
          ],
        },
      ],
    },
  });

  console.log('✓ 01_storage_stack — all tests passed');
}

// =====================================================================
// 02 — GlueStack
// =====================================================================
{
  interface GlueStackProps extends cdk.StackProps {
    rawBucket: s3.Bucket;
    processedBucket: s3.Bucket;
    scriptsBucket: s3.Bucket;
  }

  class GlueStack extends cdk.Stack {
    readonly jobName: string;
    readonly crawlerName: string;
    readonly databaseName: string;

    constructor(scope: Construct, id: string, props: GlueStackProps) {
      super(scope, id, props);

      this.databaseName = 'practice_db';

      new glue.CfnDatabase(this, 'PracticeDatabase', {
        catalogId: this.account,
        databaseInput: { name: this.databaseName },
      });

      // ── Glue ETL job role ──────────────────────────────────────────────
      const glueJobRole = new iam.Role(this, 'GlueJobRole', {
        assumedBy: new iam.ServicePrincipal('glue.amazonaws.com'),
        managedPolicies: [
          iam.ManagedPolicy.fromAwsManagedPolicyName('service-role/AWSGlueServiceRole'),
        ],
      });
      props.rawBucket.grantRead(glueJobRole);
      props.processedBucket.grantReadWrite(glueJobRole);

      const job = new glue.CfnJob(this, 'TransformJob', {
        name: 'practice-transform-job',
        role: glueJobRole.roleArn,
        command: {
          name:           'glueetl',
          pythonVersion:  '3',
          scriptLocation: `s3://${props.scriptsBucket.bucketName}/jobs/transform.py`,
        },
        glueVersion:     '4.0',
        workerType:      'G.1X',
        numberOfWorkers: 2,
      });
      this.jobName = job.name!;

      // ── Crawler role + crawler ──────────────────────────────────────────
      const crawlerRole = new iam.Role(this, 'GlueCrawlerRole', {
        assumedBy: new iam.ServicePrincipal('glue.amazonaws.com'),
        managedPolicies: [
          iam.ManagedPolicy.fromAwsManagedPolicyName('service-role/AWSGlueServiceRole'),
        ],
      });
      props.processedBucket.grantRead(crawlerRole);

      const crawler = new glue.CfnCrawler(this, 'ProcessedCrawler', {
        name:         'practice-crawler',
        role:         crawlerRole.roleArn,
        databaseName: this.databaseName,
        targets: {
          s3Targets: [{ path: `s3://${props.processedBucket.bucketName}/processed/` }],
        },
        schemaChangePolicy: { updateBehavior: 'LOG', deleteBehavior: 'LOG' },
      });
      this.crawlerName = crawler.name!;
    }
  }

  const app = new cdk.App();
  const helperStack = new cdk.Stack(app, 'Buckets');
  const rawBucket       = new s3.Bucket(helperStack, 'Raw');
  const processedBucket = new s3.Bucket(helperStack, 'Processed');
  const scriptsBucket   = new s3.Bucket(helperStack, 'Scripts');

  const glueStack = new GlueStack(app, 'TestGlue', { rawBucket, processedBucket, scriptsBucket });
  const template = Template.fromStack(glueStack);

  template.resourceCountIs('AWS::Glue::Database', 1);
  template.resourceCountIs('AWS::Glue::Job', 1);
  template.resourceCountIs('AWS::Glue::Crawler', 1);

  template.hasResourceProperties('AWS::IAM::Role', {
    AssumeRolePolicyDocument: {
      Statement: [
        { Action: 'sts:AssumeRole', Principal: { Service: 'glue.amazonaws.com' } },
      ],
    },
  });

  template.hasResourceProperties('AWS::Glue::Job', {
    Command: { Name: 'glueetl', PythonVersion: '3' },
    GlueVersion: '4.0',
  });

  console.log('✓ 02_glue_stack — all tests passed');
}

// =====================================================================
// 03 — OrchestrationStack
// =====================================================================
{
  interface OrchestrationStackProps extends cdk.StackProps {
    glueJobName: string;
    crawlerName: string;
  }

  class OrchestrationStack extends cdk.Stack {
    readonly stateMachineArn: string;

    constructor(scope: Construct, id: string, props: OrchestrationStackProps) {
      super(scope, id, props);

      const pipelineSucceeded = new sfn.Succeed(this, 'PipelineSucceeded');
      const pipelineFailed = new sfn.Fail(this, 'PipelineFailed', {
        error: 'PracticePipelineError',
        cause: 'One or more steps failed',
      });

      // ── Glue ETL job (sync) ──────────────────────────────────────────────
      const runGlueJob = new tasks.GlueStartJobRun(this, 'RunGlueETLJob', {
        glueJobName: props.glueJobName,
        integrationPattern: sfn.IntegrationPattern.RUN_JOB,
        resultPath: '$.glueResult',
      });
      runGlueJob.addCatch(pipelineFailed, { errors: ['States.ALL'] });

      // ── Crawler polling loop ────────────────────────────────────────────
      const waitForCrawler = new sfn.Wait(this, 'WaitForCrawler', {
        time: sfn.WaitTime.duration(cdk.Duration.seconds(30)),
      });

      const getCrawlerStatus = new tasks.CallAwsService(this, 'GetCrawlerStatus', {
        service: 'glue',
        action: 'getCrawler',
        parameters: { Name: props.crawlerName },
        iamResources: [`arn:aws:glue:${this.region}:${this.account}:crawler/${props.crawlerName}`],
        resultSelector: { 'state.$': '$.Crawler.State' },
        resultPath: '$.crawlerStatus',
      });

      const crawlerDone = new sfn.Choice(this, 'CrawlerFinished?')
        .when(sfn.Condition.stringEquals('$.crawlerStatus.state', 'READY'), pipelineSucceeded)
        .when(sfn.Condition.stringEquals('$.crawlerStatus.state', 'RUNNING'), waitForCrawler)
        .otherwise(pipelineFailed);

      waitForCrawler.next(getCrawlerStatus).next(crawlerDone);
      runGlueJob.next(waitForCrawler);

      // ── State machine ────────────────────────────────────────────────────
      const stateMachine = new sfn.StateMachine(this, 'PracticeStateMachine', {
        stateMachineName: 'practice-pipeline',
        definitionBody: sfn.DefinitionBody.fromChainable(runGlueJob),
        stateMachineType: sfn.StateMachineType.STANDARD,
        timeout: cdk.Duration.hours(1),
      });
      this.stateMachineArn = stateMachine.stateMachineArn;
    }
  }

  const app = new cdk.App();
  const orchestration = new OrchestrationStack(app, 'TestOrchestration', {
    glueJobName: 'practice-transform-job',
    crawlerName: 'practice-crawler',
  });
  const template = Template.fromStack(orchestration);

  template.resourceCountIs('AWS::StepFunctions::StateMachine', 1);
  template.hasResourceProperties('AWS::StepFunctions::StateMachine', {
    StateMachineType: 'STANDARD',
  });

  const json = JSON.stringify(template.toJSON());
  for (const stateName of ['RunGlueETLJob', 'WaitForCrawler', 'GetCrawlerStatus', 'CrawlerFinished?', 'PipelineSucceeded', 'PipelineFailed']) {
    console.assert(json.includes(stateName), `definition missing state: ${stateName}`);
  }

  console.log('✓ 03_orchestration_stack — all tests passed');
}

// =====================================================================
// 04 — app.ts wiring
// =====================================================================
{
  class StorageStack extends cdk.Stack {
    readonly processedBucket: s3.Bucket;

    constructor(scope: Construct, id: string, props?: cdk.StackProps) {
      super(scope, id, props);

      this.processedBucket = new s3.Bucket(this, 'ProcessedBucket', {
        removalPolicy:     cdk.RemovalPolicy.DESTROY,
        autoDeleteObjects: true,
      });
    }
  }

  interface GlueStackProps extends cdk.StackProps {
    processedBucket: s3.Bucket;
  }

  class GlueStack extends cdk.Stack {
    readonly jobName: string;

    constructor(scope: Construct, id: string, props: GlueStackProps) {
      super(scope, id, props);

      this.jobName = 'practice-transform-job';

      new glue.CfnJob(this, 'TransformJob', {
        name: this.jobName,
        role: 'arn:aws:iam::123456789012:role/placeholder',
        command: {
          name:           'glueetl',
          pythonVersion:  '3',
          scriptLocation: `s3://${props.processedBucket.bucketName}/jobs/transform.py`,
        },
        glueVersion: '4.0',
      });
    }
  }

  interface OrchestrationStackProps extends cdk.StackProps {
    glueJobName: string;
  }

  class OrchestrationStack extends cdk.Stack {
    constructor(scope: Construct, id: string, props: OrchestrationStackProps) {
      super(scope, id, props);
      new cdk.CfnOutput(this, 'WiredGlueJobName', { value: props.glueJobName });
    }
  }

  // ── The actual "app.ts" wiring ────────────────────────────────────────
  const app = new cdk.App();

  const env: cdk.Environment = {
    account: process.env.CDK_DEFAULT_ACCOUNT,
    region:  process.env.CDK_DEFAULT_REGION ?? 'us-east-1',
  };

  const storage = new StorageStack(app, 'PracticeStorage', { env });

  const glueStack = new GlueStack(app, 'PracticeGlue', {
    env,
    processedBucket: storage.processedBucket,
  });

  new OrchestrationStack(app, 'PracticeOrchestration', {
    env,
    glueJobName: glueStack.jobName,
  });

  app.synth();

  const glueTemplate = Template.fromStack(glueStack);
  const glueJson = JSON.stringify(glueTemplate.toJSON());
  console.assert(glueJson.includes('Fn::ImportValue'), 'GlueStack should import a value from StorageStack');

  const orchTemplate = Template.fromStack(app.node.findChild('PracticeOrchestration') as cdk.Stack);
  orchTemplate.hasOutput('WiredGlueJobName', { Value: 'practice-transform-job' });

  console.log('✓ 04_app_wiring — all tests passed');
}
