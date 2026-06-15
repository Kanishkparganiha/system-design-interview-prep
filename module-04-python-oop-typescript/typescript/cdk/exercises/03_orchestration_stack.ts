/**
 * CDK Exercise 03 — Step Functions: the "OrchestrationStack" pattern
 * =====================================================================
 *
 * CONCEPTS:
 *   - sfn.Succeed / sfn.Fail   → terminal states. Define these FIRST since
 *     earlier states reference them (`.next(pipelineFailed)`).
 *   - tasks.GlueStartJobRun    → a built-in Step Functions <-> Glue integration.
 *     `integrationPattern: RUN_JOB` (".sync" in ASL) means Step Functions calls
 *     StartJobRun, then polls GetJobRun for you — no manual Wait/Choice loop needed.
 *   - .addCatch(state, { errors }) → if the task fails, transition here instead
 *     of letting the whole execution die with an unhandled error.
 *   - sfn.Wait + tasks.CallAwsService + sfn.Choice → the manual polling pattern,
 *     used when there's NO built-in ".sync" integration (e.g. Glue Crawlers).
 *     Wait → call a status-check API → Choice branches back to Wait (loop) or
 *     forward (done).
 *   - sfn.Condition.stringEquals('$.path', 'VALUE') → branch on JSON state.
 *   - DefinitionBody.fromChainable(firstState) → CDK walks `.next()` links from
 *     `firstState` and discovers every connected state — you never manually
 *     register states in a list.
 *   - sfn.StateMachine → StateMachineType.STANDARD (long-running, exactly-once)
 *     vs EXPRESS (≤5 min, cheaper, at-least-once).
 *
 * REAL-WORLD REFERENCE:
 *   This mirrors lib/orchestration-stack.ts in aws-etl-pipeline-cdk — "Stack 4".
 *   The real one chains: RunGlueETLJob → StartCrawler → (Wait/Choice loop) →
 *   TriggerSMProcessing → (Wait/Choice loop) → Succeed/Fail. This exercise
 *   builds a shorter version: RunGlueETLJob → (crawler Wait/Choice loop) → Succeed/Fail.
 *
 * RUN:
 *   cd typescript/cdk && npm install   (if you haven't already)
 *   npx tsx exercises/03_orchestration_stack.ts
 */

import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as sfn from 'aws-cdk-lib/aws-stepfunctions';
import * as tasks from 'aws-cdk-lib/aws-stepfunctions-tasks';
import { Template } from 'aws-cdk-lib/assertions';

// ---- EXAMPLE (for reference) ----
//
// The smallest possible state machine: one Pass state straight to Succeed.
// `DefinitionBody.fromChainable(pass)` is how CDK turns a chain of `.next()`
// calls into the ASL (Amazon States Language) JSON that Step Functions runs.
class HelloWorldStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const done = new sfn.Succeed(this, 'Done');
    const sayHello = new sfn.Pass(this, 'SayHello', {
      result: sfn.Result.fromString('hello'),
    });
    sayHello.next(done);

    new sfn.StateMachine(this, 'HelloStateMachine', {
      definitionBody: sfn.DefinitionBody.fromChainable(sayHello),
    });
  }
}

// ---- TASK 1: Props + terminal states ----
//
// interface OrchestrationStackProps extends cdk.StackProps {
//   glueJobName: string;
//   crawlerName: string;
// }
//
// Inside the stack constructor, define (in this order, since later states
// reference them):
//   const pipelineSucceeded = new sfn.Succeed(this, 'PipelineSucceeded', {...})
//   const pipelineFailed    = new sfn.Fail(this, 'PipelineFailed', {
//     error: 'PracticePipelineError',
//     cause: 'One or more steps failed',
//   })

// YOUR CODE HERE

interface OrchestrationStackProps extends cdk.StackProps {
  // ...
}

class OrchestrationStack extends cdk.Stack {
  readonly stateMachineArn: string = ''; // overwrite in constructor

  constructor(scope: Construct, id: string, props: OrchestrationStackProps) {
    super(scope, id, props);

    // const pipelineSucceeded = ...
    // const pipelineFailed = ...

    // ---- TASK 2: Glue job step (sync integration + error catch) ----
    //
    // const runGlueJob = new tasks.GlueStartJobRun(this, 'RunGlueETLJob', {
    //   glueJobName: props.glueJobName,
    //   integrationPattern: sfn.IntegrationPattern.RUN_JOB,
    //   resultPath: '$.glueResult',
    // });
    // runGlueJob.addCatch(pipelineFailed, { errors: ['States.ALL'] });
    //
    // (don't call .next() yet — Task 3 builds what comes after)

    // YOUR CODE HERE

    // ---- TASK 3: Crawler status polling loop (Wait → CallAwsService → Choice) ----
    //
    // const waitForCrawler = new sfn.Wait(this, 'WaitForCrawler', {
    //   time: sfn.WaitTime.duration(cdk.Duration.seconds(30)),
    // });
    //
    // const getCrawlerStatus = new tasks.CallAwsService(this, 'GetCrawlerStatus', {
    //   service: 'glue',
    //   action: 'getCrawler',
    //   parameters: { Name: props.crawlerName },
    //   iamResources: [`arn:aws:glue:${this.region}:${this.account}:crawler/${props.crawlerName}`],
    //   resultSelector: { 'state.$': '$.Crawler.State' },
    //   resultPath: '$.crawlerStatus',
    // });
    //
    // const crawlerDone = new sfn.Choice(this, 'CrawlerFinished?')
    //   .when(sfn.Condition.stringEquals('$.crawlerStatus.state', 'READY'), pipelineSucceeded)
    //   .when(sfn.Condition.stringEquals('$.crawlerStatus.state', 'RUNNING'), waitForCrawler)
    //   .otherwise(pipelineFailed);
    //
    // waitForCrawler.next(getCrawlerStatus).next(crawlerDone);
    //
    // Then connect Task 2's output to this loop:
    //   runGlueJob.next(waitForCrawler);

    // YOUR CODE HERE

    // ---- TASK 4: StateMachine ----
    //
    // const stateMachine = new sfn.StateMachine(this, 'PracticeStateMachine', {
    //   stateMachineName: 'practice-pipeline',
    //   definitionBody: sfn.DefinitionBody.fromChainable(runGlueJob),
    //   stateMachineType: sfn.StateMachineType.STANDARD,
    //   timeout: cdk.Duration.hours(1),
    // });
    // this.stateMachineArn = stateMachine.stateMachineArn;

    // YOUR CODE HERE
  }
}

// ---- TASK 5: Instantiate ----

// YOUR CODE HERE
// const app = new cdk.App();
// const orchestration = new OrchestrationStack(app, 'TestOrchestration', {
//   glueJobName: 'practice-transform-job',
//   crawlerName: 'practice-crawler',
// });

// ---- TESTS ---- (uncomment after implementing)

/*
const template = Template.fromStack(orchestration);

// Exactly one state machine, of type STANDARD
template.resourceCountIs('AWS::StepFunctions::StateMachine', 1);
template.hasResourceProperties('AWS::StepFunctions::StateMachine', {
  StateMachineType: 'STANDARD',
});

// The definition (a big JSON string built via Fn::Join) should reference
// every state we created. Stringify the whole template and look for the
// state NAMES — a quick way to sanity-check the chain without parsing ASL.
const json = JSON.stringify(template.toJSON());
for (const stateName of ['RunGlueETLJob', 'WaitForCrawler', 'GetCrawlerStatus', 'CrawlerFinished?', 'PipelineSucceeded', 'PipelineFailed']) {
  console.assert(json.includes(stateName), `definition missing state: ${stateName}`);
}

console.log('✓ 03_orchestration_stack — all tests passed');
*/

void HelloWorldStack; // suppress unused-variable lint for the EXAMPLE class
